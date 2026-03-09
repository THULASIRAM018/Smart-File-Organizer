import { Folder } from 'lucide-react';

const FolderSelector = ({ folderPath, setFolderPath, disabled }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-200 hover:border-pink-300 transition-all duration-200">
      <label htmlFor="folder" className="block text-lg font-bold text-gray-800 mb-3">
        Select Folder Path
      </label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Folder className="h-5 w-5 text-yellow-500" />
        </div>
        <input
          type="text"
          id="folder"
          value={folderPath}
          onChange={(e) => setFolderPath(e.target.value)}
          className="w-full pl-12 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-4 focus:ring-yellow-300 focus:border-yellow-500 transition-all duration-200 outline-none"
          placeholder="e.g., C:\Users\username\Desktop\MyFolder"
          disabled={disabled}
        />
      </div>
      <p className="mt-2 text-sm text-gray-500">
        Enter the full path to the folder you want to organize
      </p>
    </div>
  );
};

export default FolderSelector;
