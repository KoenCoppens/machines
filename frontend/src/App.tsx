import { Link, Route, Routes } from "react-router-dom";
import AccountsList from "./pages/AccountsList";
import AccountDetail from "./pages/AccountDetail";
import AlertsInbox from "./pages/AlertsInbox";

const App = () => {
  return (
    <div className="app">
      <header className="topbar">
        <div className="logo">Machine Management</div>
        <nav>
          <Link to="/">Accounts</Link>
          <Link to="/alerts">Alerts Inbox</Link>
        </nav>
      </header>
      <main className="container">
        <Routes>
          <Route path="/" element={<AccountsList />} />
          <Route path="/accounts/:id" element={<AccountDetail />} />
          <Route path="/alerts" element={<AlertsInbox />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
