import re
from nltk import corpus
stop_words = set(corpus.stopwords.words())

author_ratios = []
title_ratios = []
abstract_ratios = []


def get_ratio_stops(text):
    text_list = filter(bool, re.split(r'<lb/>|\s', text))
    ratio = 1. * len(filter(lambda x: x in stop_words, text_list)) / len(text_list)
    return ratio


abstracts = ["""
a b s t r a c t<lb/> The absence of a neutrino flux from self-annihilating dark matter captured in the Sun has tightly con-<lb/>strained some leading particle dark matter scenarios. The impact of astrophysical uncertainties on the<lb/> capture process of dark matter in the Sun and hence also the derived constraints by neutrino telescopes<lb/> need to be taken into account. In this review we have explored relevant uncertainties in solar WIMP<lb/> searches, summarized results from leading experiments, and provided an outlook into upcoming searches<lb/> and future experiments. We have created an interactive plotting tool that allows the user to view current<lb/> limits and projected sensitivities of major experiments under changing astrophysical conditions.<lb/>
""",
"""Abstract. In [BBK10] it was shown how so-called wonderful compactifica-<lb/>tions can be used for renormalization in the position space formulation of<lb/> quantum field theory. This article aims to continue this idea, using a slightly<lb/> different approach; instead of the subspaces in the arrangement of divergent<lb/> loci, we use the poset of divergent subgraphs as the main tool to describe the<lb/> whole renormalization process. This is based on [Fei05] where wonderful mod-<lb/>els were studied from a purely combinatorial viewpoint. The main motivation<lb/> for this approach is the fact that both, renormalization and the model con-<lb/>struction, are governed by the combinatorics of this poset. Not only simplifies<lb/> this the exposition considerably, but also allows to study the renormalization<lb/> operators in more detail. Moreover, we explore the renormalization group in<lb/> this setting by studying how the renormalized distributions behave under a<lb/> change of renormalization points.<lb/>
""",
"""Abstract<lb/> Performance evolution of parameters achieved during<lb/> the electromagnetic design of the longitudinal kicker<lb/> cavity for the LNLS UVX storage ring is presented. The<lb/> effort on the electromagnetic optimization process of the<lb/> heavily loaded cavity has been made to reach the required<lb/> electrodynamic parameters of the kicker. The results for<lb/> three different geometries are compared and a good<lb/> compromise between the longitudinal shunt impedance<lb/> and the effect of the longitudinal Higher Order Modes<lb/> (HOM&apos;s) on beam stability has been found.<lb/>
""",
"""Abstract<lb/> A supersymmetric extension of the Hunter-Saxton equation is constructed. We<lb/> present its bi-Hamiltonian structure and show that it arises geometrically as a<lb/> geodesic equation on the space of superdiffeomorphisms of the circle that leave<lb/> a point fixed endowed with a right-invariant metric.<lb/> AMS Subject Classification (2000): 37K10, 17A70.<lb/>
""",
"""In this paper, from a given Kuper-CH spectral problem, we propose two kinds of<lb/> super integrable hierarchies. One is the Kuper-CH hierarchy, the other is the gen-<lb/>eralized Kuper-Harry-Dym hierarchy. Moreover, we construct their zero curvature<lb/> representations and super-bi-Hamiltonian structures.
""",
"""A super Camassa–Holm equation with peakon solutions is proposed, which is<lb/> associated with a 3 × 3 matrix spectral problem with two potentials. With<lb/> the aid of the zero-curvature equation, we derive a hierarchy of super Harry<lb/> Dym type equations and establish their Hamiltonian structures. It is shown<lb/> that the super Camassa–Holm equation is exactly a negative flow in the<lb/> hierarchy and admits exact solutions with N peakons. As an example, exact<lb/> 1-peakon solutions of the super Camassa–Holm equation are given. Infinitely<lb/> many conserved quantities of the super Camassa–Holm equation and the super<lb/> Harry Dym type equation are, respectively, obtained.<lb/>
""",
"""From the super-matrix Lie algebras, we consider a super-extension of the CKdV equation hierarchy in<lb/> the present Letter, and propose the super-CKdV hierarchy with self-consistent sources. Furthermore, we<lb/> establish the infinitely many conservation laws for the integrable super-CKdV hierarchy.<lb/>
""",
"""Abstract<lb/> The Seiberg-Witten equations are of great importance in the study of topology of<lb/> smooth four-dimensional manifolds. In this work, we propose similar equations for<lb/> 7-dimensional compact manifolds with G 2 -structure.<lb/>
""",
"""The notion of self-duality of 2-forms in 4-dimensions plays an em-<lb/>inent role in many areas of mathematics and physics, but although<lb/> the 2-forms have a genuine meaning related to curvature and gauge-<lb/>field-strength in higher dimensions also, their &quot; self-duality&quot; is some-<lb/>thing which is almost avoided above 4-dimensions. We show that<lb/> self-duality of 2-forms is a very natural notion in higher (even) di-<lb/>mensions also and we prove the equivalence of some scattered and<lb/> rarely used definitions in the literature. We demonstrate the useful-<lb/>ness of this higher self-duality by studying it in 8-dimensions and<lb/> we derive a natural expression for the Bonan form in terms of self-<lb/>dual 2-forms and we give an explicit expression of the local action<lb/> of SO(8) on the Bonan form.<lb/>
""",
"""Presented are the most recent jet fragmentation results from CDF: inclusive distributions of charged particle<lb/> momenta and their k T in jets; average track multiplicities, as well as angular distributions of multiplicity flow,<lb/> for a wide range of jet energies with E T from 40 to 300 GeV. The results are compared with Monte-Carlo and,<lb/> when possible, analytical calculations performed in resummed perturbative QCD approximations (MLLA).<lb/>
""",
"""Abstract<lb/> The High Luminosity LHC upgrade program foresees a<lb/> possibility of using the second harmonic cavities working<lb/> at 800 MHz for the collider bunch length variation. Such<lb/> harmonic cavities should provide an opportunity to vary<lb/> the length of colliding bunches. In order to supply the<lb/> required harmonic voltage several single cell<lb/> superconducting cavities are to be used. Different cavity<lb/> designs and several higher order mode (HOM) damping<lb/> techniques are being studied in order to reduce the cavity<lb/> HOM impact on the beam stability and to minimize<lb/> parasitic power losses. In this paper we analyze and<lb/> compare the HOM electromagnetic characteristics and<lb/> respective wake potential decay rates for cavities with<lb/> grooves, fluted and ridged beam pipes. The problem of<lb/> Lorentz force detuning is also addressed.<lb/>
""",
"""ABSTRACT<lb/> Geometric algebra is a mathematical structure that is inherent in any metric vector space, and defined by the<lb/> requirement that the metric tensor is given by the scalar part of the product of vectors. It provides a natural<lb/> framework in which to represent the classical groups as subgroups of rotation groups, and similarly their Lie<lb/> algebras. In this article we show how the geometric algebra of a six-dimensional real Euclidean vector space<lb/> naturally allows one to construct the special unitary group on a two-qubit (quantum bit) Hilbert space, in a<lb/> fashion similar to that used in the well-established Bloch sphere model for a single qubit. This is then used to<lb/> illustrate the Cartan decompositions and subalgebras of the four-dimensional unitary group, which have recently<lb/> been used by J. Zhang, J. Vala, S. Sastry and K. B. Whaley [Phys. Rev. A 67, 042313, 2003] to study the<lb/> entangling capabilities of two-qubit unitaries.<lb/>
""",
"""Abstract<lb/> We exhibit each of the finite groups of umbral moonshine as a distinguished subgroup of<lb/> the automorphism group of a distinguished linear code, each code being defined over a different<lb/> quotient of the ring of integers. These code constructions entail permutation representations<lb/> which we use to give a description of the multiplier systems of the vector-valued mock modular<lb/> forms attached to the conjugacy classes of the umbral groups by umbral moonshine.<lb/>
""",
"""Abstract<lb/> According to the conventional knowledge, it is believed<lb/> that the nonlinearity in the arc would not reduce the beam-<lb/>beam performance, since the beam-beam force is dominated<lb/> in the beam core region while the lattice nonlinearity is dom-<lb/>inated in the beam halo region. However in the recent few<lb/> + − storage ring colliders, it has been shown that the lat-<lb/>tice nonlinearity may be important to the luminosity perfor-<lb/>mance. In this paper, we&apos;ll try to review the related story<lb/> in DAFNE, and its upgrade with crab waist scheme, KEKB,<lb/> Super-KEKB and BEPCII.<lb/>
""",
"""Abstract<lb/> The microscopic composition and the direct or indirect observation of dark matter, other than trough its gravitational<lb/> effects, is currently one of the most urgent and important problems in particle physics, astrophysics and cosmology.<lb/> Since several years ago, different kinds of experimental searches have been conducted without any conclusive<lb/> results. All the evidence shows that the microscopic constituents of dark matter cannot belong to the particle spectrum<lb/> of the Standard Model. Several other theoretical models provide candidates to be the constituents of this kind of<lb/> matter, among them some versions of supersymmetric models, in which the lightest neutralinos are stable, neutral,<lb/> massive and do not have color charge, making them excellent candidates. The LHC experiments have conducted<lb/> thorough searches of supersymmetric particles during the first runs of the LHC at 7 and 8 TeV, without any positive<lb/> result. These searches have been concentrated in strong production channels, with gluinos and s-quarks in the final<lb/> state. Given the negative results, it is necessary to perform detailed searches in electro-weak channels in which the<lb/> supersymmetric particles in the final state are expected to be lighter, and therefore, have higher probability to be<lb/> produced, including the neutralinos. The supersymmetric production channels mediated by vector boson fusion are<lb/> the most promising ones. In this article, a review of the dark matter searches performed during the first runs of the<lb/> LHC are presented, making emphasis on the vector boson fusion channels, as well as the strategies for the searches<lb/> to be performed in the next run, at 14 TeV.<lb/> Ciencias físicas<lb/>
""",
"""Abstract<lb/> This paper is focused on HOM damping in 9-cell<lb/> superconducting cavities. We are considering HOM<lb/> propagation outside from the cavity ridged and fluted drift<lb/> tubes. The analysis of the influence of the parameters of<lb/> the drift tube on the HOM damping was conducted. The<lb/> considered methods were analysed and compared.<lb/>
""",
"""a b s t r a c t<lb/> In this note, we first give a quick presentation of the supergeometry underlying<lb/> supergravity theories, using an intrinsic differential geometric language. For this, we adopt<lb/> the point of view of Cartan geometries, and rely as well on the work of John Lott, who has<lb/> found a unified geometrical interpretation of the torsion constraints for many supergravity<lb/> theories, based on the use of H-structures. In this framework, the constraints amount to<lb/> requiring first-order integrability of H-structures, for a specific supergroup H.<lb/> The supergroup H used by Lott is not the usual diagonal representation of the Lorentz<lb/> group on superspace, but an extension of the latter. This extension appears to be natural<lb/> and it can be related to the super-Poincaré group. We also observe that the constraints<lb/> arising from the requirement of first-order integrability have basically the same form, in<lb/> any spacetime dimension.<lb/> Looking at supergravity from an affine viewpoint (i.e. as a gauge theory for the<lb/> super-Poincaré group), we show that requiring first-order integrability amounts to<lb/> requiring the equivalence, up to gauge transformations, between infinitesimal gauge<lb/> supertranslations acting on the supervielbein and infinitesimal superdiffeomorphisms<lb/> acting on the supervielbein.<lb/> The latter action is performed through a covariant Lie derivative, whose expression<lb/> involves naturally the supertorsion tensor. We use this expression to show that the term<lb/> added to the spin connection, in the supercovariant derivative of d = 11 supergravity, has<lb/> a natural superspace origin. In particular, the 4-form field strength is related to a specific<lb/> component of the supertorsion tensor.<lb/> We conclude by some general remarks concerning Killing spinors in geometry and<lb/> supergravity, discussing their possible interpretations, as Killing vector fields on a specific<lb/> supermanifold on one hand, and as parallel spinors for an appropriate connection on the<lb/> other hand. We show that this last interpretation is very natural from the point of view of<lb/> Klein and Cartan geometries.<lb/>
""",
"""We derive an encoded universality representation for a generalized anisotropic exchange Hamil-<lb/>tonian that contains cross-product terms in addition to the usual two-particle exchange terms. The<lb/> recently developed algebraic approach is used to show that the minimal universality-generating en-<lb/>codings of one logical qubit are based on three physical qubits. We show how to generate both<lb/> single-and two-qubit operations on the logical qubits, using suitably timed conjugating operations<lb/> derived from analysis of the commutator algebra. The timing of the operations is seen to be crucial<lb/> in allowing simplification of the gate sequences for the generalized Hamiltonian to forms similar<lb/> to that derived previously for the symmetric (XY) anisotropic exchange Hamiltonian. The total<lb/> number of operations needed for a controlled-Z gate up to local transformations is five. A scalable<lb/> architecture is proposed.<lb/>
""",
"""Abstract<lb/> The LHC High Luminosity upgrade program considers<lb/> an option of using additional cavities, operating at<lb/> multiplies of the main RF system frequency of 400 MHz.<lb/> Such harmonic cavities should provide a possibility to<lb/> vary the length of colliding bunches. In order to supply<lb/> the required harmonic voltage several single cell<lb/> superconducting cavities are to be used. It is desirable to<lb/> house more cavities in a single cryostat to reduce the<lb/> number of transitions between &quot;warm&quot; and &quot;cold&quot; parts of<lb/> the cryogenic system. In this paper we study<lb/> electromagnetic characteristics of a chain of the single<lb/> cell superconducting cavities coupled by drifts tubes. In<lb/> order to reduce the influence of Higher order modes<lb/> (HOM) excited in the structure on the beam stability and<lb/> to minimize eventual power losses we analyze the HOM<lb/> parameters and calculate the wake potential decay rates<lb/> due to application of different HOM damping devices. In<lb/> particular, the methods of HOM damping with<lb/> rectangular waveguides connected to the drift tubes, the<lb/> loads placed in the fluted and ridged drift tubes, as well as<lb/> combinations of these methods are compared.<lb/>
""",
"""Abstract. Classically, starting from the Witt and Virasoro algebra im-<lb/>portant examples of Lie superalgebras were constructed. In this write-up<lb/> of a talk presented at the Biaa lowie˙ za meetings we report on results on<lb/> Lie superalgebras of Krichever-Novikov type. These algebras are multi-<lb/>point and higher genus equivalents of the classical algebras. The grading<lb/> in the classical case is replaced by an almost-grading. It is induced by<lb/> a splitting of the set of points, were poles are allowed, into two disjoint<lb/> subsets. With respect to a fixed splitting, or equivalently with respect<lb/> to a fixed almost-grading, it is shown that there is up to rescaling and<lb/> equivalence a unique non-trivial central extension of the Lie superalge-<lb/>bra of Krichever–Novikov type. It is given explicitly.<lb/>
"""]

authors = [
"""Matthias Danninger<lb/> a, * , Carsten Rott<lb/> b<lb/>
""",
"""MARKO BERGHOFF<lb/>
""",
"""L. Sanfelici<lb/> #<lb/> , H. O. C. Duarte, S. R. Marques, 
""",
"""J. Lenells<lb/>
""",
"""Ling Zhang<lb/> 1,2,a) and Dafeng Zuo<lb/> 1,3,b)<lb/>
""",
"""By Xianguo Geng, Bo Xue, and Lihua Wu<lb/>
""",
"""Li Li *<lb/>
""",
"""Nedim DĚ<lb/> GIRMENCI and Nülifer¨OZDEMIR<lb/>
""",
"""Ay¸se Hümeyra Bilge<lb/> a, * , Tekin Dereli<lb/> b , ¸<lb/> Sahin Koçak<lb/> c<lb/>
""",
"""Alexei Safonov<lb/>
""",
"""Ya.V. Shashkov, N.P. Sobenin
""",
"""Timothy F. Havel a and Chris J. L. Doran b<lb/> a
""",
"""John F. R. Duncan *<lb/>
""",
"""Y. Zhang †<lb/>, 
""",
"""Juan Carlos Sanabria<lb/>
""",
"""A. Mitrofanov, Ya.Shashkov, N. Sobenin,
""",
"""Michel Egeileh<lb/> a, * , Fida El Chami<lb/> b<lb/>
""",
"""Jiri Vala and K. Birgitta Whaley<lb/>
""",
"""Ya.V. Shashkov, N.P. Sobenin  M.M. Zobov,
""",
"""Martin Schlichenmaier<lb/>
"""]

titles = [
"""Solar WIMPs unravelled: Experiments, astrophysical uncertainties,<lb/> and interactive tools<lb/>
""",
"""WONDERFUL COMPACIFICATIONS IN QUANTUM FIELD<lb/> THEORY<lb/>
""",
"""DESIGN AND IMPEDANCE OPTIMIZATION OF THE LNLS-UVX<lb/> LONGITUDINAL KICKER CAVITY<lb/>
""",
"""A bi-Hamiltonian Supersymmetric Geodesic<lb/> Equation<lb/>
""",
"""Integrable hierarchies related to the Kuper-CH<lb/> spectral problem<lb/>
""",
"""A Super Camassa–Holm Equation with N-Peakon<lb/> Solutions<lb/>
""",
"""Conservation laws and self-consistent sources for a super-CKdV equation hierarchy<lb/>
""",
"""Seiberg-Witten-like Equations on 7-Manifolds<lb/> with G 2 -Structure<lb/>
""",
"""Maximal linear subspaces of strong self-dual 2-forms and the<lb/> Bonan 4-form<lb/>
""",
"""Fragmentation of CDF jets: perturbative or non-perturbative?<lb/>
""",
"""ANALYSIS OF HIGH ORDER MODES DAMPING TECHNIQUES FOR 800<lb/> MHZ SINGLE CELL SUPERCONDUCTING CAVITIES*<lb/>
""",
"""A Bloch-Sphere-Type Model for Two Qubits in the<lb/> Geometric Algebra of a 6-D Euclidean Vector Space<lb/>
""",
"""Umbral Moonshine and Linear Codes<lb/>
""",
"""REVIEW OF CROSSTALK BETWEEN BEAM-BEAM INTERACTION<lb/> AND LATTICE NONLINEARITY IN + − COLLIDERS *<lb/>
""",
"""Búsquedas de Materia Oscura Supersimétrica en el LHC<lb/>
""",
"""HIGHER ORDER MODES DAMPING FOR 9-CELL STRUCTURE WITH<lb/> MODIFIED DRIFT TUBE<lb/>
""",
"""Some remarks on the geometry of superspace supergravity<lb/>
""",
"""Encoded Universality for Generalized Anisotropic Exchange Hamiltonians<lb/>
""",
"""COMPARSION OF HIGHER ORDER MODES DAMPING TECHNIQUES<lb/> FOR AN ARRAY OF SINGLE CELL CAVITIES<lb/>
""",
"""Lie superalgebras of Krichever–Novikov type<lb/>
"""]

for i in range(len(authors)):
    abstract_ratios.append(get_ratio_stops(abstracts[i]))
    author_ratios.append(get_ratio_stops(authors[i]))
    title_ratios.append(get_ratio_stops(titles[i]))


# [0.37719298245614036,  # Abstract
#  0.4206896551724138,
#  0.3875,
#  0.3673469387755102,
#  0.35,
#  0.32,
#  0.358974358974359,
#  0.3125,
#  0.4296875,
#  0.3181818181818182,
#  0.29838709677419356,
#  0.3881578947368421,
#  0.4166666666666667,
#  0.4,
#  0.4046692607003891,
#  0.35294117647058826,
#  0.41904761904761906,
#  0.33587786259541985,
#  0.3516483516483517,
#  0.408,
#  0.1111111111111111,  # Authors
#  0.0,
#  0.0,
#  0.0,
#  0.25,
#  0.14285714285714285,
#  0.3,
#  0.25,
#  0.2727272727272727,
#  0.2857142857142857,
#  0.0,
#  0.3125,
#  0.2,
#  0.0,
#  0.375,
#  0.0,
#  0.375,
#  0.14285714285714285,
#  0.0,
#  0.2,
#  0.0,  # Titles
#  0.0,
#  0.0,
#  0.0,
#  0.14285714285714285,
#  0.125,
#  0.0,
#  0.2,
#  0.07142857142857142,
#  0.0,
#  0.0,
#  0.2727272727272727,
#  0.0,
#  0.0,
#  0.0,
#  0.0,
#  0.0,
#  0.16666666666666666,
#  0.0,
#  0.0]
