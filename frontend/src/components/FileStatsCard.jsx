const FileStatsCard = ({ title, value, icon: Icon, color }) => {
  const colorClasses = {
    pink: 'bg-pink-100 text-pink-600 border-pink-300',
    blue: 'bg-blue-100 text-blue-600 border-blue-300',
    green: 'bg-green-100 text-green-600 border-green-300',
    yellow: 'bg-yellow-100 text-yellow-600 border-yellow-300',
    purple: 'bg-purple-100 text-purple-600 border-purple-300',
    orange: 'bg-orange-100 text-orange-600 border-orange-300',
  };

  return (
    <div className={`${colorClasses[color]} rounded-xl shadow-lg p-6 border-2 transition-all duration-200 hover:scale-105 hover:shadow-xl`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold opacity-80 uppercase tracking-wide">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`p-4 rounded-full ${colorClasses[color]} bg-opacity-50`}>
          <Icon className="h-8 w-8" />
        </div>
      </div>
    </div>
  );
};

export default FileStatsCard;
