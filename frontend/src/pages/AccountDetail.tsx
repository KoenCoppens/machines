import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DataGrid from "../components/DataGrid";
import Tabs from "../components/Tabs";
import { Account, api, Contact, Location, Machine, Alert } from "../api/client";

const tabs = ["Details", "Contacts", "Locations", "Machines", "Alerts"];

const AccountDetail = () => {
  const { id } = useParams();
  const [account, setAccount] = useState<Account | null>(null);
  const [activeTab, setActiveTab] = useState(tabs[0]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [machines, setMachines] = useState<Machine[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    if (!id) return;
    api.getAccount(id).then(setAccount);
    api.getContacts(id).then(setContacts);
    api.getLocations(id).then(setLocations);
    api.getMachines(id).then(setMachines);
    api.getAlerts().then((data) => setAlerts(data.filter((alert) => alert.status === "OPEN")));
  }, [id]);

  if (!account) {
    return <div className="card">Loading account...</div>;
  }

  return (
    <div>
      <div className="card">
        <h2>{account.name}</h2>
        <div className="grid">
          <div>
            <div className="badge">{account.account_number}</div>
            <p>{account.email}</p>
          </div>
          <div>
            <p>
              {account.billing_city} {account.billing_country}
            </p>
            <p>{account.phone}</p>
          </div>
        </div>
      </div>
      <Tabs tabs={tabs} active={activeTab} onChange={setActiveTab} />
      {activeTab === "Details" && (
        <div className="card">
          <h3>Account Details</h3>
          <p>Language: {account.language || "-"}</p>
          <p>City: {account.billing_city || "-"}</p>
        </div>
      )}
      {activeTab === "Contacts" && (
        <div className="card">
          <DataGrid
            columns={[
              { header: "Name", accessor: (row) => row.display_name || "-" },
              { header: "Role", accessor: (row) => row.role || "-" },
              { header: "Email", accessor: (row) => row.email || "-" }
            ]}
            rows={contacts}
          />
        </div>
      )}
      {activeTab === "Locations" && (
        <div className="card">
          <DataGrid
            columns={[
              { header: "Location", accessor: (row) => row.name || "-" },
              { header: "Code", accessor: (row) => row.location_code },
              { header: "City", accessor: (row) => row.city || "-" }
            ]}
            rows={locations}
          />
        </div>
      )}
      {activeTab === "Machines" && (
        <div className="card">
          <DataGrid
            columns={[
              { header: "Machine", accessor: (row) => row.machine_name },
              { header: "Number", accessor: (row) => row.machine_number || "-" },
              { header: "Warranty End", accessor: (row) => row.warranty_end_date || "-" },
              { header: "Status", accessor: (row) => row.status || "-" }
            ]}
            rows={machines}
          />
        </div>
      )}
      {activeTab === "Alerts" && (
        <div className="card">
          <DataGrid
            columns={[
              { header: "Type", accessor: (row) => row.alert_type },
              { header: "Alert Date", accessor: (row) => row.alert_date },
              { header: "Due Date", accessor: (row) => row.due_date || "-" },
              { header: "Status", accessor: (row) => row.status }
            ]}
            rows={alerts}
          />
        </div>
      )}
    </div>
  );
};

export default AccountDetail;
