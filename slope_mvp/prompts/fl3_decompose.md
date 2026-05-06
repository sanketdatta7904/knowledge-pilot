You are enumerating the parametric cases of a math sub-skill (FL2 → FL3).

FL3 is NOT further decomposition into smaller skills. It is case enumeration — the same skill applied under different parameter conditions (sign of a coefficient, special values, edge cases).

Guidelines:
- Most FL2s split into 2 cases by the sign of a key parameter (e.g. m>0 vs m<0, or b>0 vs b<0).
- If the FL2 has NO meaningful parametric cases, return an empty list.
- For each case, write a description that includes the condition, e.g. "construct a readable slope triangle when m>0".
- Set `parametric_condition` to a short label like "m>0" or "b<0".

Examples:
- FL2 "construct a readable slope triangle on a line"
  → FL3 [{description: "...when m>0", parametric_condition: "m>0"},
         {description: "...when m<0", parametric_condition: "m<0"}]
- FL2 "mark the y-intercept"
  → FL3 [] (no meaningful parametric split — y-intercept is just a point)

Return only descriptions and parametric_condition.
