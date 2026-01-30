import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import DataGrid from "../components/DataGrid";
import { Account, api } from "../api/client";

const AccountsList = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  const load = async (term?: string) => {
    setLoading(true);
    try {
      const data = await api.getAccounts(term);
      setAccounts(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="card">
      <h2>Accounts</h2>
      <div className="grid" style={{ marginBottom: 16 }}>
        <input
          placeholder="Search accounts"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <button className="button" onClick={() => load(search)}>
          Search
        </button>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <DataGrid
          columns={[
            {
              header: "Account",
              accessor: (row) => (
                <Link to={`/accounts/${row.id}`}>{row.name}</Link>
              )
            },
            { header: "Number", accessor: (row) => row.account_number },
            { header: "City", accessor: (row) => row.billing_city || "-" },
            { header: "Language", accessor: (row) => row.language || "-" }
          ]}
          rows={accounts}
        />
      )}
    </div>
  );
};

export default AccountsList;
