(function (root) {
  "use strict";

  function stateOf(values) {
    if (!Array.isArray(values) || values.length === 0) return "U";
    if (values.some(value => value === "R")) return "R";
    if (values.some(value => value === "U")) return "U";
    if (values.every(value => value === "C")) return "C";
    throw new Error("El estado debe ser C, R o U.");
  }

  function evaluate(input) {
    const accessibility = stateOf([input.economy, input.institution, input.family]);
    const compatibility = stateOf([input.time]);
    const sustainability = stateOf([input.continuity, input.family]);
    const life = stateOf([accessibility, compatibility, sustainability]);
    const expansion = stateOf([input.equity, input.externalCost, input.rights]);
    return { accessibility, compatibility, sustainability, life, expansion };
  }

  root.ARCHITECTURES_RULES = Object.freeze({ stateOf, evaluate });
})(typeof window === "undefined" ? globalThis : window);
