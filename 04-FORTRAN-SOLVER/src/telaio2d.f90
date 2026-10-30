! =============================================================================
!  telaio2d — solutore per telai piani, statica lineare (metodo degli spostamenti)
!  Progetto Alessandra · 04-FORTRAN-SOLVER · v0.2 (30/10/2026)
!
!  Uso:   telaio2d  input.txt  output.txt  [piena]
!         (piena: eliminazione di Gauss a matrice piena, per confronto)
!
!  Ingresso ASCII scritto dal convertitore (03-BACKEND/converter/converti.py).
!  Unità coerenti m, kN. Carichi d'asta già in componenti LOCALI.
!
!    TELAIO2D 1
!    NODI n            → id x y
!    ASTE m            → id ni nj E A I ril_i ril_j          (ril = 1 cerniera)
!    VINCOLI k         → nodo ux uy rz kx ky kr              (0/1, molle)
!    CARICHI_NODALI p  → nodo Fx Fy Mz
!    CARICHI_ASTE q    → asta tipo wx wy a                   (tipo 1 uniforme, 2 concentrato)
!    FINE
!
!  Uscita: SPOSTAMENTI, REAZIONI, ESTREMITA (forze d'estremità locali
!  f1..f6 = Fx_i Fy_i M_i Fx_j Fy_j M_j agenti sull'asta), ROTAZIONI_ASTE
!  (rotazioni delle due estremità di ogni asta: diverse da quelle dei nodi
!  solo dove c'è una cerniera interna; difetto D8, 30/10).
!
!  Convenzioni identiche a 01-ARCHITETTURA/DATA_SCHEMA.json.
!  Sistema risolto con Cholesky a banda (30/10, Elisa e Ottavia): memoria
!  proporzionale a n·b e tempo a n·b², con b semibanda dipendente dalla
!  numerazione dei nodi. L'opzione «piena» conserva il metodo della v0.1.
! =============================================================================
program telaio2d
   implicit none
   integer, parameter :: dp = kind(1.0d0)

   integer :: nn, ne, nv, ncn, nca, ndof, i, j, k, a, b, ios, u_in, u_out, hb, nr, rr(2)
   integer, allocatable :: nid(:), eid(:), eni(:), enj(:), ril(:,:)
   integer, allocatable :: vnodo(:), vfix(:,:), cnn(:), cae(:), cat(:)
   real(dp), allocatable :: x(:), y(:), eE(:), eA(:), eI(:), vk(:,:)
   real(dp), allocatable :: cnf(:,:), caw(:,:)
   real(dp), allocatable :: Kb(:,:), Kf(:,:), Fv(:), Fn(:), Uv(:), Fll(:), Rku(:), molk(:)
   logical, allocatable :: vinc(:), molla(:)
   integer, allocatable :: eq(:), dofs(:,:)
   real(dp), allocatable :: elL(:), elc(:), els(:), kc(:,:,:), fc(:,:), k0(:,:,:), f0(:,:)
   real(dp) :: kl(6,6), ff(6), T(6,6), kg(6,6), fg(6), ul(6), fe(6), ug(6), phi(6), A2(2,2), b2(2), det
   real(dp) :: dx, dy, L
   integer :: nlib
   logical :: piena
   character(len=256) :: fin, fout, tag, opz
   character(len=32) :: hdr

   if (command_argument_count() < 2 .or. command_argument_count() > 3) then
      write(*,'(a)') 'Uso: telaio2d input.txt output.txt [piena]'
      stop 1
   end if
   call get_command_argument(1, fin)
   call get_command_argument(2, fout)
   piena = .false.
   if (command_argument_count() == 3) then
      call get_command_argument(3, opz)
      if (trim(opz) /= 'piena') call errore('opzione sconosciuta: '//trim(opz))
      piena = .true.
   end if

   open(newunit=u_in, file=trim(fin), status='old', action='read', iostat=ios)
   if (ios /= 0) call errore('impossibile aprire il file di ingresso')

   read(u_in,*) hdr, i
   if (trim(hdr) /= 'TELAIO2D' .or. i /= 1) call errore('intestazione non riconosciuta')

   read(u_in,*) tag, nn
   call controlla(tag, 'NODI')
   allocate(nid(nn), x(nn), y(nn))
   do i = 1, nn
      read(u_in,*) nid(i), x(i), y(i)
   end do

   read(u_in,*) tag, ne
   call controlla(tag, 'ASTE')
   allocate(eid(ne), eni(ne), enj(ne), eE(ne), eA(ne), eI(ne), ril(2,ne))
   do i = 1, ne
      read(u_in,*) eid(i), eni(i), enj(i), eE(i), eA(i), eI(i), ril(1,i), ril(2,i)
   end do

   read(u_in,*) tag, nv
   call controlla(tag, 'VINCOLI')
   allocate(vnodo(nv), vfix(3,nv), vk(3,nv))
   do i = 1, nv
      read(u_in,*) vnodo(i), vfix(1,i), vfix(2,i), vfix(3,i), vk(1,i), vk(2,i), vk(3,i)
   end do

   read(u_in,*) tag, ncn
   call controlla(tag, 'CARICHI_NODALI')
   allocate(cnn(ncn), cnf(3,ncn))
   do i = 1, ncn
      read(u_in,*) cnn(i), cnf(1,i), cnf(2,i), cnf(3,i)
   end do

   read(u_in,*) tag, nca
   call controlla(tag, 'CARICHI_ASTE')
   allocate(cae(nca), cat(nca), caw(3,nca))
   do i = 1, nca
      read(u_in,*) cae(i), cat(i), caw(1,i), caw(2,i), caw(3,i)
   end do
   close(u_in)

   ! controlli di coerenza dei riferimenti (revisione di Marisa, 28/10)
   do k = 1, nca
      if (count(eid == cae(k)) /= 1) call errore('carico su un''asta inesistente')
   end do
   do k = 1, ne
      if (count(eid == eid(k)) /= 1) call errore('identificativi delle aste duplicati')
   end do
   do k = 1, nn
      if (count(nid == nid(k)) /= 1) call errore('identificativi dei nodi duplicati')
   end do

   ! ---------------------------------------------------------------- vincoli e numerazione
   ndof = 3*nn
   allocate(Fv(ndof), Fn(ndof), Uv(ndof), Rku(ndof), molk(ndof), vinc(ndof), molla(ndof), eq(ndof))
   allocate(dofs(6,ne), elL(ne), elc(ne), els(ne), kc(6,6,ne), fc(6,ne), k0(6,6,ne), f0(6,ne))
   Fv = 0; Fn = 0; Uv = 0; molk = 0
   vinc = .false.; molla = .false.
   do k = 1, nv
      i = indice(vnodo(k))
      do a = 1, 3
         if (vfix(a,k) == 1) vinc(3*i-3+a) = .true.
         if (vk(a,k) > 0) then
            molk(3*i-3+a) = molk(3*i-3+a) + vk(a,k)
            molla(3*i-3+a) = .true.
         end if
      end do
   end do
   ! equazioni solo per i gradi di libertà liberi, nell'ordine dei nodi
   nlib = 0; eq = 0
   do a = 1, ndof
      if (.not. vinc(a)) then
         nlib = nlib + 1; eq(a) = nlib
      end if
   end do

   ! ---------------------------------------------------------------- rigidezze d'asta
   hb = 0
   do k = 1, ne
      i = indice(eni(k)); j = indice(enj(k))
      dx = x(j) - x(i); dy = y(j) - y(i)
      L = sqrt(dx*dx + dy*dy)
      if (L <= 0) call errore('asta di lunghezza nulla')
      elL(k) = L; elc(k) = dx/L; els(k) = dy/L
      call rig_locale(eE(k), eA(k), eI(k), L, kl)
      call incastro(k, L, ff)
      k0(:,:,k) = kl; f0(:,k) = ff
      call condensa(kl, ff, ril(:,k))
      kc(:,:,k) = kl; fc(:,k) = ff
      dofs(:,k) = [3*i-2, 3*i-1, 3*i, 3*j-2, 3*j-1, 3*j]
      do a = 1, 6
         do b = 1, 6
            if (eq(dofs(a,k)) > 0 .and. eq(dofs(b,k)) > 0) hb = max(hb, eq(dofs(b,k)) - eq(dofs(a,k)))
         end do
      end do
   end do

   ! ---------------------------------------------------------------- assemblaggio
   ! limite di memoria della matrice a banda: 5·10⁷ termini (400 MB). Il convertitore riordina i nodi
   ! (Cuthill-McKee inverso) per contenere la semibanda; il limite protegge da file scritti a mano.
   if (.not. piena .and. real(hb+1, dp)*real(nlib, dp) > 5.0e7_dp) &
      call errore('semibanda troppo grande: riordinare i nodi o ridurre il modello')
   if (piena) then
      allocate(Kf(nlib,nlib)); Kf = 0
   else
      allocate(Kb(0:hb,nlib)); Kb = 0
   end if
   do k = 1, ne
      call rotazione(elc(k), els(k), T)
      kg = matmul(transpose(T), matmul(kc(:,:,k), T))
      fg = matmul(transpose(T), fc(:,k))
      do a = 1, 6
         Fv(dofs(a,k)) = Fv(dofs(a,k)) - fg(a)
         do b = 1, 6
            call somma(eq(dofs(a,k)), eq(dofs(b,k)), kg(a,b))
         end do
      end do
   end do
   do a = 1, ndof
      if (molla(a)) call somma(eq(a), eq(a), molk(a))
   end do

   do k = 1, ncn
      i = indice(cnn(k))
      Fn(3*i-2:3*i) = Fn(3*i-2:3*i) + cnf(:,k)
   end do
   Fv = Fv + Fn

   ! ---------------------------------------------------------------- soluzione
   allocate(Fll(nlib))
   Fll = pack(Fv, .not. vinc)
   if (piena) then
      call gauss(Kf, Fll, nlib)
   else
      call cholesky_banda(Kb, Fll, nlib, hb)
   end if
   Uv = unpack(Fll, .not. vinc, 0.0_dp)

   ! reazioni = somma delle forze d'asta nei nodi − carichi nodali (molle escluse dalla rigidezza)
   Rku = 0
   do k = 1, ne
      call rotazione(elc(k), els(k), T)
      ul = matmul(T, Uv(dofs(:,k)))
      fe = matmul(kc(:,:,k), ul) + fc(:,k)
      Rku(dofs(:,k)) = Rku(dofs(:,k)) + matmul(transpose(T), fe)
   end do
   Rku = Rku - Fn

   ! ---------------------------------------------------------------- uscita
   open(newunit=u_out, file=trim(fout), status='replace', action='write')
   write(u_out,'(a,1x,i0)') 'SPOSTAMENTI', nn
   do i = 1, nn
      write(u_out,'(i0,3(1x,es24.16))') nid(i), Uv(3*i-2), Uv(3*i-1), Uv(3*i)
   end do
   write(u_out,'(a,1x,i0)') 'REAZIONI', count([(any(vinc(3*i-2:3*i)) .or. any(molla(3*i-2:3*i)), i = 1, nn)])
   do i = 1, nn
      if (any(vinc(3*i-2:3*i)) .or. any(molla(3*i-2:3*i))) then
         write(u_out,'(i0,3(1x,es24.16))') nid(i), (reazione(3*i-3+a), a = 1, 3)
      end if
   end do
   write(u_out,'(a,1x,i0)') 'ESTREMITA', ne
   do k = 1, ne
      call rotazione(elc(k), els(k), T)
      ug = Uv(dofs(:,k))
      ul = matmul(T, ug)
      fe = matmul(kc(:,:,k), ul) + fc(:,k)
      write(u_out,'(i0,6(1x,es24.16))') eid(k), fe
   end do
   write(u_out,'(a,1x,i0)') 'ROTAZIONI_ASTE', ne
   do k = 1, ne
      call rotazione(elc(k), els(k), T)
      ul = matmul(T, Uv(dofs(:,k)))
      phi = ul
      ! rotazioni svincolate: equilibrio dei momenti d'estremità nulli sull'asta non condensata
      nr = 0
      do a = 1, 2
         if (ril(a,k) == 1) then
            nr = nr + 1; rr(nr) = 3*a
         end if
      end do
      do a = 1, nr
         phi(rr(a)) = 0
      end do
      if (nr == 1) then
         phi(rr(1)) = -(dot_product(k0(rr(1),:,k), phi) + f0(rr(1),k))/k0(rr(1),rr(1),k)
      else if (nr == 2) then
         A2 = k0(rr, rr, k)
         b2 = -(matmul(k0(rr,:,k), phi) + f0(rr,k))
         det = A2(1,1)*A2(2,2) - A2(1,2)*A2(2,1)
         phi(3) = (b2(1)*A2(2,2) - A2(1,2)*b2(2))/det
         phi(6) = (A2(1,1)*b2(2) - A2(2,1)*b2(1))/det
      end if
      write(u_out,'(i0,2(1x,es24.16))') eid(k), phi(3), phi(6)
   end do
   write(u_out,'(a)') 'FINE'
   close(u_out)

contains

   real(dp) function reazione(d)
      integer, intent(in) :: d
      if (vinc(d) .or. molla(d)) then
         reazione = Rku(d)
      else
         reazione = 0
      end if
   end function

   integer function indice(id)
      integer, intent(in) :: id
      integer :: q
      do q = 1, nn
         if (nid(q) == id) then
            indice = q
            return
         end if
      end do
      call errore('nodo non definito')
      indice = 0
   end function

   subroutine controlla(t, atteso)
      character(len=*), intent(in) :: t, atteso
      if (trim(t) /= atteso) call errore('sezione attesa: '//atteso)
   end subroutine

   subroutine errore(msg)
      character(len=*), intent(in) :: msg
      write(0,'(a)') 'ERRORE telaio2d: '//msg
      stop 2
   end subroutine

   subroutine rig_locale(Em, Ar, In, Lu, kl)
      real(dp), intent(in) :: Em, Ar, In, Lu
      real(dp), intent(out) :: kl(6,6)
      real(dp) :: s1, s2, s3, s4, s5
      s1 = Em*Ar/Lu; s2 = 12*Em*In/Lu**3; s3 = 6*Em*In/Lu**2; s4 = 4*Em*In/Lu; s5 = 2*Em*In/Lu
      kl = 0
      kl(1,1) = s1;  kl(1,4) = -s1; kl(4,1) = -s1; kl(4,4) = s1
      kl(2,2) = s2;  kl(2,3) = s3;  kl(2,5) = -s2; kl(2,6) = s3
      kl(3,2) = s3;  kl(3,3) = s4;  kl(3,5) = -s3; kl(3,6) = s5
      kl(5,2) = -s2; kl(5,3) = -s3; kl(5,5) = s2;  kl(5,6) = -s3
      kl(6,2) = s3;  kl(6,3) = s5;  kl(6,5) = -s3; kl(6,6) = s4
   end subroutine

   subroutine rotazione(c, s, T)
      real(dp), intent(in) :: c, s
      real(dp), intent(out) :: T(6,6)
      T = 0
      T(1,1) = c;  T(1,2) = s;  T(2,1) = -s; T(2,2) = c;  T(3,3) = 1
      T(4,4) = c;  T(4,5) = s;  T(5,4) = -s; T(5,5) = c;  T(6,6) = 1
   end subroutine

   subroutine incastro(el, L, f)
      integer, intent(in) :: el
      real(dp), intent(in) :: L
      real(dp), intent(out) :: f(6)
      real(dp) :: wx, wy, pa, pb
      integer :: q
      f = 0
      do q = 1, nca
         if (cae(q) /= eid(el)) cycle
         wx = caw(1,q); wy = caw(2,q)
         if (cat(q) == 1) then
            f(1) = f(1) - wx*L/2;  f(4) = f(4) - wx*L/2
            f(2) = f(2) - wy*L/2;  f(5) = f(5) - wy*L/2
            f(3) = f(3) - wy*L**2/12;  f(6) = f(6) + wy*L**2/12
         else
            pa = caw(3,q); pb = L - pa
            if (pa < 0 .or. pa > L) call errore('carico concentrato fuori dall''asta')
            f(1) = f(1) - wx*pb/L;  f(4) = f(4) - wx*pa/L
            f(2) = f(2) - wy*pb**2*(3*pa + pb)/L**3
            f(5) = f(5) - wy*pa**2*(pa + 3*pb)/L**3
            f(3) = f(3) - wy*pa*pb**2/L**2
            f(6) = f(6) + wy*pa**2*pb/L**2
         end if
      end do
   end subroutine

   subroutine condensa(kl, f, r)
      ! Condensazione statica delle rotazioni svincolate (gdl 3 e/o 6)
      real(dp), intent(inout) :: kl(6,6), f(6)
      integer, intent(in) :: r(2)
      integer :: p, q, ia, ib
      do p = 1, 2
         if (r(p) /= 1) cycle
         q = 3*p
         if (abs(kl(q,q)) < tiny(1.0_dp)) cycle
         do ia = 1, 6
            if (ia == q) cycle
            do ib = 1, 6
               if (ib == q) cycle
               kl(ia,ib) = kl(ia,ib) - kl(ia,q)*kl(q,ib)/kl(q,q)
            end do
            f(ia) = f(ia) - kl(ia,q)*f(q)/kl(q,q)
         end do
         kl(q,:) = 0; kl(:,q) = 0; f(q) = 0
      end do
   end subroutine

   subroutine somma(p, q, v)
      ! aggiunge v al termine (p,q) della matrice dei gradi di libertà liberi
      integer, intent(in) :: p, q
      real(dp), intent(in) :: v
      if (p == 0 .or. q == 0) return
      if (piena) then
         Kf(p,q) = Kf(p,q) + v
      else if (q >= p) then
         Kb(q-p,p) = Kb(q-p,p) + v
      end if
   end subroutine

   subroutine cholesky_banda(B, f, n, h)
      ! K = Uᵀ U con K simmetrica definita positiva in forma a banda superiore:
      ! B(d,i) = K(i,i+d), d = 0..h. Pivot non positivo o trascurabile → struttura labile.
      integer, intent(in) :: n, h
      real(dp), intent(inout) :: B(0:h,n), f(n)
      integer :: p, q, r
      real(dp) :: sm, dmax
      dmax = max(tiny(1.0_dp), maxval(abs(B(0,:))))
      do p = 1, n
         sm = B(0,p)
         do r = max(1,p-h), p-1
            sm = sm - B(p-r,r)**2
         end do
         if (sm <= 1.0e-12_dp*dmax) call errore('matrice singolare: struttura labile o vincoli insufficienti')
         B(0,p) = sqrt(sm)
         do q = p+1, min(n,p+h)
            sm = B(q-p,p)
            do r = max(1,q-h), p-1
               sm = sm - B(p-r,r)*B(q-r,r)
            end do
            B(q-p,p) = sm/B(0,p)
         end do
      end do
      do p = 1, n
         sm = f(p)
         do r = max(1,p-h), p-1
            sm = sm - B(p-r,r)*f(r)
         end do
         f(p) = sm/B(0,p)
      end do
      do p = n, 1, -1
         sm = f(p)
         do q = p+1, min(n,p+h)
            sm = sm - B(q-p,p)*f(q)
         end do
         f(p) = sm/B(0,p)
      end do
   end subroutine

   subroutine gauss(A, bvec, n)
      integer, intent(in) :: n
      real(dp), intent(inout) :: A(n,n), bvec(n)
      integer :: c, p, r
      real(dp) :: fct, amax, tmp(n), tb
      amax = maxval(abs(A))
      do c = 1, n
         p = c - 1 + maxloc(abs(A(c:n,c)), dim=1)
         if (abs(A(p,c)) < 1.0e-12_dp*max(1.0_dp, amax)) &
            call errore('matrice singolare: struttura labile o vincoli insufficienti')
         if (p /= c) then
            tmp = A(c,:); A(c,:) = A(p,:); A(p,:) = tmp
            tb = bvec(c); bvec(c) = bvec(p); bvec(p) = tb
         end if
         do r = c + 1, n
            fct = A(r,c)/A(c,c)
            if (fct /= 0) then
               A(r,c:n) = A(r,c:n) - fct*A(c,c:n)
               bvec(r) = bvec(r) - fct*bvec(c)
            end if
         end do
      end do
      do r = n, 1, -1
         bvec(r) = (bvec(r) - dot_product(A(r,r+1:n), bvec(r+1:n)))/A(r,r)
      end do
   end subroutine

end program telaio2d
