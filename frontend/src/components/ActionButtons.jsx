import { Scan, FolderCheck } from 'lucide-react';

const ActionButtons = ({ onScan, onOrganize, loading, disabled }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <button
        onClick={onScan}
        disabled={disabled || loading}
        className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-4 px-6 rounded-xl font-bold text-lg hover:from-blue-600 hover:to-cyan-600 transition-all duration-200 flex items-center justify-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:scale-105"
      >
        {loading === 'scan' ? (
          <>
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
            <span>Scanning...</span>
          </>
        ) : (
          <>
            <Scan className="h-6 w-6" />
            <span>Scan Files</span>
          </>
        )}
      </button>

      <button
        onClick={onOrganize}
        disabled={disabled || loading}
        className="bg-gradient-to-r from-green-500 to-emerald-500 text-white py-4 px-6 rounded-xl font-bold text-lg hover:from-green-600 hover:to-emerald-600 transition-all duration-200 flex items-center justify-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:scale-105"
      >
        {loading === 'organize' ? (
          <>
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
            <span>Organizing...</span>
          </>
        ) : (
          <>
            <FolderCheck className="h-6 w-6" />
            <span>Organize Files</span>
          </>
        )}
      </button>
    </div>
  );
};

export default ActionButtons;
