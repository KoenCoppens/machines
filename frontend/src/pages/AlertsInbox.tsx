import { useEffect, useState } from "react";
import DataGrid from "../components/DataGrid";
import { Alert, api } from "../api/client";

const AlertsInbox = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const load = async () => {
    const data = await api.getAlerts("OPEN");
    setAlerts(data);
  };

  useEffect(() => {
    load();
  }, []);

  const markDone = async (id: string) => {
    await api.updateAlert(id, { status: "DONE" });
    load();
  };

  const snooze = async (id: string) => {
    const snoozeUntil = new Date();
    snoozeUntil.setDate(snoozeUntil.getDate() + 7);
    await api.updateAlert(id, { snooze_until: snoozeUntil.toISOString().slice(0, 10) });
    load();
  };

  const assign = async (id: string) => {
    await api.updateAlert(id, { assigned_to: "field.team@poc.local" });
    load();
  };

  return (
    <div className="card">
      <h2>Alerts Inbox</h2>
      <DataGrid
        columns={[
          { header: "Type", accessor: (row) => row.alert_type },
          { header: "Alert Date", accessor: (row) => row.alert_date },
          { header: "Due Date", accessor: (row) => row.due_date || "-" },
          { header: "Assigned", accessor: (row) => row.assigned_to || "Unassigned" },
          {
            header: "Actions",
            accessor: (row) => (
              <div style={{ display: "flex", gap: 8 }}>
                <button className="button" onClick={() => markDone(row.id)}>
                  Done
                </button>
                <button className="button secondary" onClick={() => snooze(row.id)}>
                  Snooze
                </button>
                <button className="button secondary" onClick={() => assign(row.id)}>
                  Assign
                </button>
              </div>
            )
          }
        ]}
        rows={alerts}
      />
    </div>
  );
};

export default AlertsInbox;
