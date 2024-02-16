import { BrowserRouter, Routes, Route, createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";
import './App.css';
import {AppMenu} from './components/AppMenu';
import ViewMessagesPage from "./pages/ViewMessagesPage";
import HomePage from "./pages/HomePage";
import ConnectionPage from "./pages/ConnectionPage";
import ManagePage from "./pages/ManagePage";
import UserPage from "./pages/UserPage";
import Error404Page from "./pages/Error404Page";


function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <header className="app-bar">
          <h1 className="app-name">PFE Messagerie</h1>
          <AppMenu />
        </header>
        <div className="app-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="manage" element={<ManagePage />} />
            <Route path="messages" element={<ViewMessagesPage />} />
            <Route path="connection" element={<ConnectionPage />} />
            <Route path="user" element={<UserPage />} />
            <Route path="*" element={<Error404Page />} />
          </Routes>
          <Outlet />
        </div>
      </div>
    </BrowserRouter>
  );

}

export default App;
