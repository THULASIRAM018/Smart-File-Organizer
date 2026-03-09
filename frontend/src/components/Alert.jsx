import { CheckCircle, XCircle, X } from 'lucide-react';

const Alert = ({ type, message, onClose }) => {
  const types = {
    success: {
      bg: 'bg-green-50 border-green-500',
      text: 'text-green-800',
      icon: CheckCircle,
      iconColor: 'text-green-500',
    },
    error: {
      bg: 'bg-red-50 border-red-500',
      text: 'text-red-800',
      icon: XCircle,
      iconColor: 'text-red-500',
    },
  };

  const config = types[type];
  const Icon = config.icon;

  return (
    <div className={`${config.bg} border-l-4 p-4 rounded-lg shadow-md mb-6 flex items-start justify-between`}>
      <div className="flex items-start space-x-3">
        <Icon className={`h-5 w-5 ${config.iconColor} mt-0.5`} />
        <p className={`${config.text} font-medium`}>{message}</p>
      </div>
      <button
        onClick={onClose}
        className={`${config.text} hover:opacity-70 transition-opacity duration-200`}
      >
        <X className="h-5 w-5" />
      </button>
    </div>
  );
};

export default Alert;
