@echo off

npx playwright test tests/generated/payment.spec.ts --workers=1 --reporter=line