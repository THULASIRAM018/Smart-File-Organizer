import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import FolderSelector from '../components/FolderSelector';
import ActionButtons from '../components/ActionButtons';
import FileStatsCard from '../components/FileStatsCard';
import Alert from '../components/Alert';
import { fileAPI } from '../services/api';
import { FileText, Folder, CheckCircle, Clock } from 'lucide-react';

const Dashboard = () => {
  const [folderPath, setFolderPath] = useState('');
  const [loading, setLoading] = useState(null);
  const [alert, setAlert] = useState(null);
  const [stats, setStats] = useState({
    totalFiles: 0,
    organized: 0,
    pending: 0,
    categories: 0,
  });
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
    }
  }, [navigate]);

  const handleScan = async () => {
    if (!folderPath) {
      setAlert({ type: 'error', message: 'Please enter a folder path' });
      return;
    }

    setLoading('scan');
    setAlert(null);

    try {
      const response = await fileAPI.scanFiles(folderPath);
      const data = response.data;

      setStats({
        totalFiles: data.total_files || 0,
        organized: data.organized || 0,
        pending: data.pending || data.total_files || 0,
        categories: data.categories || 0,
      });

      setAlert({
        type: 'success',
        message: `Scan completed! Found ${data.total_files || 0} files.`,
      });
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.message || 'Failed to scan files. Please check the folder path.',
      });
    } finally {
      setLoading(null);
    }
  };

  const handleOrganize = async () => {
    if (!folderPath) {
      setAlert({ type: 'error', message: 'Please enter a folder path' });
      return;
    }

    setLoading('organize');
    setAlert(null);

    try {
      const response = await fileAPI.organizeFiles(folderPath);
      const data = response.data;

      setStats({
        totalFiles: data.total_files || stats.totalFiles,
        organized: data.organized || stats.totalFiles,
        pending: 0,
        categories: data.categories || stats.categories,
      });

      setAlert({
        type: 'success',
        message: `Files organized successfully! ${data.organized || stats.totalFiles} files have been organized.`,
      });
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.message || 'Failed to organize files. Please try again.',
      });
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-yellow-50 to-blue-50">
      <Navbar isAuthenticated={true} />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Dashboard
          </h1>
          <p className="text-gray-600 text-lg">
            Manage and organize your files efficiently
          </p>
        </div>

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <FileStatsCard
            title="Total Files"
            value={stats.totalFiles}
            icon={FileText}
            color="blue"
          />
          <FileStatsCard
            title="Organized"
            value={stats.organized}
            icon={CheckCircle}
            color="green"
          />
          <FileStatsCard
            title="Pending"
            value={stats.pending}
            icon={Clock}
            color="orange"
          />
          <FileStatsCard
            title="Categories"
            value={stats.categories}
            icon={Folder}
            color="purple"
          />
        </div>

        <div className="space-y-6">
          <FolderSelector
            folderPath={folderPath}
            setFolderPath={setFolderPath}
            disabled={loading !== null}
          />

          <ActionButtons
            onScan={handleScan}
            onOrganize={handleOrganize}
            loading={loading}
            disabled={!folderPath}
          />
        </div>

        <div className="mt-8 bg-white rounded-xl shadow-lg p-6 border-2 border-gray-200">
          <h3 className="text-xl font-bold text-gray-800 mb-4">How it works</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-3">
              <div className="bg-blue-100 text-blue-600 rounded-full p-2 flex-shrink-0">
                <span className="font-bold text-sm">1</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-800">Scan Files</h4>
                <p className="text-sm text-gray-600">
                  Analyze the folder structure and detect all files
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-green-100 text-green-600 rounded-full p-2 flex-shrink-0">
                <span className="font-bold text-sm">2</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-800">Organize Files</h4>
                <p className="text-sm text-gray-600">
                  Automatically sort files into appropriate categories
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
