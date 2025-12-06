# CASCADE
# → If the parent is deleted, all child records depending on it will also be deleted automatically.
# → Risky for inventory systems because deleting a supplier or product may delete stock or sales history.

# PROTECT
# → Prevents deleting the parent if any child records exist.
# → Django raises a ProtectedError.
# → Good when you don't want to delete things that have historical importance (purchase orders, sales).

# SET_NULL
# → If the parent is deleted, the foreign key is set to NULL.
# → Child record remains but without a parent.
# → Useful for optional relationships like category or primary supplier.

# SET_DEFAULT
# → When parent is deleted, Django sets the foreign key to its default value.
# → Use only if you have a meaningful default parent (like a default category).

# DO_NOTHING
# → No action is taken when the parent is deleted.
# → Dangerous because it can create invalid references in the database.
# → Only use if you manage constraints manually (rare).

# RESTRICT
# → Prevents deletion of the parent if child records exist (similar to PROTECT).
# → Enforced at the database level for stronger safety.
# → Best for financial, historical, or critical audit-related data (sales, stock, purchases).
