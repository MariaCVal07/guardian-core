@echo off

npx playwright test tests/generated/guardian_generated.spec.ts --workers=1 --reporter=line

exit