# %%

import numpy as np
from sympy import *
from IPython.display import display, Latex


# list of symbolic representation
He, Hl, Ve, Vl, Hte, Hre, Htl, Hrl, Vte, Vre, Vtl, Vrl, = symbols('H^e H^l V^e V^l H_t^e H_r^e H_t^l H_r^l V_t^e V_r^e V_t^l V_r^l', commutative=False)

#for simplication in the output display format
sqrt_half = Rational(1,2)**Rational(1,2)

psi_minus_early  = sqrt_half * (He * Ve - Ve * He)
psi_minus_later  = sqrt_half * (Hl * Vl - Vl * Hl)

H_transform_e    = sqrt_half * (Hte + Hre)
V_transform_e    = sqrt_half * (Vte + Vre)

H_transform_l    = sqrt_half * (Htl + Hrl)
V_transform_l    = sqrt_half * (Vtl + Vrl)

psi_bs_applied_e = psi_minus_early.subs({He: H_transform_e, Ve: V_transform_e})
psi_bs_applied_l = psi_minus_later.subs({Hl: H_transform_l, Vl: V_transform_l})

# Expand and simplify
psi_bs_applied_e = simplify(expand(psi_bs_applied_e))
psi_bs_applied_l = simplify(expand(psi_bs_applied_l))

# Display result
display(Latex(r'$\psi^-_{\text{early,transformed}} = ' + latex(psi_bs_applied_e) + r'$'))
display(Latex(r'$\psi^-_{\text{later,transformed}} = ' + latex(psi_bs_applied_l) + r'$'))

psi_minus_output_bs1 = psi_bs_applied_e * psi_bs_applied_l
psi_minus_output_bs1 = simplify(expand(psi_minus_output_bs1))
display(Latex(r'$\psi^-_{\text{BS1}} = ' + latex(psi_minus_output_bs1) + r'$'))


import re as regex

# Ensure fully expanded
terms      = expand(psi_minus_output_bs1)
term_list  = terms.args if isinstance(terms, Add) else [terms]

# Count '_r^' and '_t^' using string methods (faster & simpler)
def even_r_and_t_filter(τϵρμ):
    τϵρμ_str = str(τϵρμ)
    return τϵρμ_str.count('_r^') == 2 and τϵρμ_str.count('_t^') == 2

# Filter terms: keep only those with 2 reflected + 2 transmitted photons
# filtered_terms = [term for term in term_list if even_r_and_t_filter(term)]

filtered_terms = []
for i in term_list:
    if even_r_and_t_filter(i):
        filtered_terms.append(i)

# Recombine and simplify
even_terms = simplify(sum(filtered_terms))

# Display
display(Latex(r'$\psi^-_{\text{BS1, even\ terms}} = ' + latex(even_terms) + r'$'))


import pandas as pd

# Split even_terms into individual terms
term_data = []

for i in filtered_terms:
    coeff, expr = i.as_coeff_Mul()  # Separate coefficient and symbolic part
    term_data.append((str(expr), coeff))  # Store as (term string, coeff as Rational)

# Create DataFrame
df = pd.DataFrame(term_data, columns=['Term', 'Coefficient'])

# Save as CSV
df.to_csv("bs1_even_terms.csv", index=False)
print("CSV saved as 'bs1_even_terms.csv'")

