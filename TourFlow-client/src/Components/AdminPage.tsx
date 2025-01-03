import NewDestination from "./NewDestination";
import NavigationBar from "./NavigationBar";
import AdminNavBar from "./AdminNavBar";
import ToursManagement from "./ToursManagement";
import ManageUser from "./ManageUser";
import { useState } from "react";
const AdminPage = () => {
  const [activeComponent, setActiveComponent] = useState<string>("1"); // State để lưu component đang hiển thị

  const handleNavigation = (componentId: string) => {
    setActiveComponent(componentId); // Cập nhật state dựa trên nút được bấm
  };
  return (
    <div>
      <NavigationBar />
      <AdminNavBar onNavigate={handleNavigation} />
      <div>
        {activeComponent === "1" && <ToursManagement />}
        {activeComponent === "2" && <NewDestination />}
        {activeComponent === "3" && <ManageUser />}
      </div>
    </div>
  );
};

export default AdminPage;
