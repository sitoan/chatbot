import styles from "../styles/AdminNavBar.module.css";

interface NavigationBarProps {
  onNavigate: (componentId: string) => void; // Prop để nhận callback
}
const AdminNavBar: React.FC<NavigationBarProps> = ({ onNavigate }) => {
  return (
    <ul id={styles.admin_navbar}>
      <li onClick={() => onNavigate("1")}>Tours Management</li>
      <li onClick={() => onNavigate("2")}>Post Tour</li>
      <li onClick={() => onNavigate("3")}>Recently accessed User</li>
    </ul>
  );
};

export default AdminNavBar;
