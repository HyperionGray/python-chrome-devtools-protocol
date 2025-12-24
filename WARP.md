# WARP Context for Python CDP Library

## Project Overview
This repository contains a Python library for Chrome DevTools Protocol (CDP) type wrappers.
It's a code generation project that creates Python bindings from official CDP specifications.

## WARP Usage Context
When using this project through WARP:

### Primary Use Cases
- Generating updated CDP bindings when Chrome DevTools Protocol changes
- Running comprehensive tests on generated code
- Building documentation for the CDP Python API
- Type checking the generated Python modules

### Performance Metrics
- **Code Generation Speed**: Time to generate all CDP modules from JSON specs
- **Test Coverage**: Percentage of generated code covered by tests  
- **Type Safety**: MyPy validation of generated type annotations
- **Import Performance**: Time to import generated modules

### Build Automation
The project uses a hybrid approach:
- **Primary**: Poetry + Makefile (standard Python toolchain)
- **Secondary**: pf tasks (organizational consistency wrappers)

### Key Performance Indicators
- Generation time for ~50 CDP domains
- Memory usage during code generation
- Test execution time across all modules
- Documentation build time

### Development Workflow
1. Update CDP JSON specifications (browser_protocol.json, js_protocol.json)
2. Run code generation (pf generate)
3. Validate with type checking (pf typecheck)
4. Run comprehensive tests (pf test)
5. Build and verify documentation (pf docs)

### Automation Notes
This project is suitable for automated builds and can be integrated into
larger CDP-dependent projects. The pf tasks provide simple, reliable
entry points for automation systems.