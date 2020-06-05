"""Module containing FunctionProperties class."""


class FunctionProperties(object):
    """
    Class containing miscellaneous variables for Approach and Approach2vN classes.

    Attributes
    ----------
    symq : bool
        For symq=False keep all equations in the kernel, and the matrix is of size N by N+1.
        For symq=True replace one equation by the normalisation condition,
        and the matrix is square N by N.
    norm_row : int
        If symq=True this row will be replaced by normalisation condition in the kernel matrix.
    solmethod : string
        String specifying the solution method of the equation L(Phi0)=0.
        The possible values are matrix inversion 'solve' and least squares 'lsqr'.
        Method 'solve' works only when symq=True.
        For matrix free methods (used when mfreeq=True) the possible values are
        'krylov', 'broyden', etc.
    itype : int
        Type of integral for first order approach calculations.
        itype=0: the principal parts are evaluated using Fortran integration package QUADPACK \
                 routine dqawc through SciPy.
        itype=1: the principal parts are kept, but approximated by digamma function valid for \
                 large bandwidth D.
        itype=2: the principal parts are neglected.
        itype=3: the principal parts are neglected and infinite bandwidth D is assumed.
    dqawc_limit : int
        For itype=0 dqawc_limit determines the maximum number of sub-intervals
        in the partition of the given integration interval.
    mfreeq : bool
        If mfreeq=True the matrix free solution method is used for first order methods.
    phi0_init : array
        For mfreeq=True the initial value of zeroth order density matrix elements.
    mtype_qd : float or complex
        Type for the many-body quantum dot Hamiltonian matrix.
    mtype_leads : float or complex
        Type for the many-body tunneling matrix Tba.
    kpnt_left, kpnt_right : int
        Number of points Ek_grid is extended to the left and the right for '2vN' approach.
    ht_ker : array
        Kernel used when performing Hilbert transform using FFT.
        It is generated using specfunc.kernel_fredriksen(n).
    emin, emax : float
        Minimal and maximal energy in the updated Ek_grid generated by neumann2py.get_grid_ext(sys).
        Note that emin<=Dmin and emax>=Dmax.
    dmin, dmax : float
        Bandedge Dmin and Dmax values of the lead electrons.
    ext_fct : float
        Multiplication factor used in neumann2py.get_grid_ext(sys), when determining emin and emax.
    suppress_err : bool
        Determines whether to print the warning when the inversion of the kernel failed.
    """

    def __init__(self,
                 kerntype='2vN', symq=True, norm_row=0, solmethod=None,
                 itype=0, dqawc_limit=10000, mfreeq=False, phi0_init=None,
                 mtype_qd=float, mtype_leads=complex, kpnt=None, dband=None):
        self.kerntype = kerntype
        self.symq = symq
        self.norm_row = norm_row
        self.solmethod = solmethod
        #
        self.itype = itype
        self.dqawc_limit = dqawc_limit
        #
        self.mfreeq = mfreeq
        self.phi0_init = phi0_init
        #
        self.mtype_qd = mtype_qd
        self.mtype_leads = mtype_leads
        #
        self.kpnt = kpnt
        self.dband = dband
        #
        self.kpnt_left = 0
        self.kpnt_right = 0
        self.ht_ker = None
        #
        self.dmin, self.dmax = 0, 0
        self.emin, self.emax = 0, 0
        self.ext_fct = 1.1
        #
        self.suppress_err = False
        self.suppress_wrn = [False]

    def print_error(self, exept):
        if not self.suppress_err:
            print("WARNING: Could not solve the linear set of equations.\n" +
                  "  Error from the solver: " + str(exept) + "\n"
                  "  The reasons for such a failure can be various:\n" +
                  "  1. Some of the transport channels may be outside the bandwidth D of the leads.\n" +
                  "     In this case removing some of the states with the method [remove_states()] will help.\n" +
                  "  2. Replacement of one of the equations with the normalisation condition.\n" +
                  "     In this case try to use different [norm_row]\n"+
                  "     or solve the linear system using [symq=False] and the solution method [solmethod='lsqr'].\n"
                  "  This warning will not be shown again.\n"
                  "  To check if the solution succeeded check the property [success].")
            self.suppress_err = True

    def print_warning(self, i, message):
        if not self.suppress_wrn[i]:
            print(message)
            self.suppress_wrn[i] = True
