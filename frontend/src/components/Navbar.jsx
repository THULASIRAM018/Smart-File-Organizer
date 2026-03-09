import { FileText, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Navbar = ({ isAuthenticated }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    navigate('/');
  };

  return (
    <nav className="bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-white p-2 rounded-lg">
              <FileText className="h-6 w-6 text-pink-500" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Smart File Organizer</h1>
              <p className="text-sm text-pink-100">Organize your files intelligently</p>
            </div>
          </div>
          {isAuthenticated && (
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 bg-white text-red-500 px-4 py-2 rounded-lg hover:bg-red-50 transition-all duration-200 font-semibold"
            >
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
