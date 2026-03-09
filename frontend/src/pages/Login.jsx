import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmailLoginForm from '../components/EmailLoginForm';
import Alert from '../components/Alert';
import { authAPI } from '../services/api';
import { Sparkles } from 'lucide-react';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (email) => {
    setLoading(true);
    setAlert(null);

    try {
      await authAPI.sendOTP(email);
      setAlert({ type: 'success', message: 'OTP sent successfully! Check your email.' });
      localStorage.setItem('email', email);
      setTimeout(() => {
        navigate('/verify-otp');
      }, 1500);
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.message || 'Failed to send OTP. Please try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-yellow-50 to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 border-t-4 border-pink-500">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full mb-4">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Welcome Back!</h2>
            <p className="text-gray-600">Sign in to access your file organizer</p>
          </div>

          {alert && (
            <Alert
              type={alert.type}
              message={alert.message}
              onClose={() => setAlert(null)}
            />
          )}

          <EmailLoginForm onSubmit={handleSubmit} loading={loading} />

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              By continuing, you agree to our Terms of Service
            </p>
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Powered by <span className="font-bold text-pink-600">Smart File Organizer</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
