# Access Control, BOLA / IDOR & Multi-Tenant Authorization

Broken Object Level Authorization (**BOLA / IDOR**) remains the #1 vulnerability in modern web applications and APIs. This guide details how to detect, audit, and systematically eliminate access control flaws.

---

## 1. The Cross-Tenant Authorization Matrix Test

During an audit, mentally (or via automated abuse tests) execute the **Cross-Tenant Matrix**:

| Scenario | Requester Context | Target Resource Context | Expected Outcome | Vulnerable Outcome |
| :--- | :--- | :--- | :---: | :---: |
| **Normal Read** | User A (`tenant_1`) | Resource X (`tenant_1`) | `200 OK` | `200 OK` |
| **Cross-User (Same Tenant)** | User A (`tenant_1`, non-admin) | Resource Y (`tenant_1`, User B) | `403 Forbidden` | `200 OK` (IDOR) |
| **Cross-Tenant Attack** | Attacker (`tenant_2`) | Resource X (`tenant_1`) | `403 / 404` | `200 OK` (**Critical BOLA**) |
| **Unauthenticated Read** | Anonymous | Resource X (`tenant_1`) | `401 Unauthorized` | `200 OK` (Broken Auth) |

---

## 2. Common Vulnerable Code Patterns by Framework

### ❌ Pattern 1: Direct ORM lookup by URL param without tenancy filter (Node / Prisma)
```typescript
// VULNERABLE: Anyone who guesses the invoice ID can read it
app.get("/api/invoices/:id", async (req, res) => {
  const invoice = await prisma.invoice.findUnique({
    where: { id: req.params.id }
  });
  return res.json(invoice);
});

// ✅ DEFENSIVE: Enforce tenancy and ownership in the query predicate
app.get("/api/invoices/:id", authenticateToken, async (req, res) => {
  const invoice = await prisma.invoice.findFirst({
    where: {
      id: req.params.id,
      organizationId: req.user.organizationId, // Tenant isolation
    }
  });
  if (!invoice) return res.status(404).json({ error: "Invoice not found" });
  return res.json(invoice);
});
```

### ❌ Pattern 2: Python / FastAPI with SQLAlchemy
```python
# VULNERABLE: Direct primary key filter ignoring current_user
@router.get("/reports/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    return report

# ✅ DEFENSIVE: Filter by owner or tenant_id
@router.get("/reports/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.tenant_id == current_user.tenant_id
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
```

---

## 3. Mass Assignment (BOPLA) Auditing

Mass Assignment occurs when client input is directly bound to internal data models or database updates.

### Audit Checklist:
1. Are controllers using `Object.assign(entity, req.body)` or `model.update(req.body)`?
2. Can a user send `{"role": "admin"}` or `{"is_verified": true}` in a `/api/profile` PUT/PATCH request?
3. Are DTOs configured to strip unknown properties automatically?

### Mitigation Pattern (TypeScript / Zod):
```typescript
const UpdateUserProfileSchema = z.object({
  fullName: z.string().min(1).max(100),
  bio: z.string().max(500).optional(),
  avatarUrl: z.string().url().optional(),
}).strict(); // 👈 .strict() rejects unexpected properties like role, balance, or tenantId
```
