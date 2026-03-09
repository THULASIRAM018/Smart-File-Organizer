import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import OTPVerificationForm from '../components/OTPVerificationForm';
import Alert from '../components/Alert';
import { authAPI } from '../services/api';
import { Lock } from 'lucide-react';

const OTPVerification = () => {
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    if (!storedEmail) {
      navigate('/');
      return;
    }
    setEmail(storedEmail);
  }, [navigate]);

  const handleSubmit = async (otp) => {
    setLoading(true);
    setAlert(null);

    try {
      const response = await authAPI.verifyOTP(email, otp);
      const token = response.data.session_token;

      if (token) {
        localStorage.setItem('token', token);
      }

      setAlert({ type: 'success', message: 'OTP verified successfully!' });
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.message || 'Invalid OTP. Please try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setAlert(null);
    try {
      await authAPI.sendOTP(email);
      setAlert({ type: 'success', message: 'OTP resent successfully!' });
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.message || 'Failed to resend OTP.',
      });
    }
  };

  if (!email) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 border-t-4 border-blue-500">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-green-500 rounded-full mb-4">
              <Lock className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Verify OTP</h2>
            <p className="text-gray-600">Enter the code we sent to your email</p>
          </div>

          {alert && (
            <Alert
              type={alert.type}
              message={alert.message}
              onClose={() => setAlert(null)}
            />
          )}

          <OTPVerificationForm
            email={email}
            onSubmit={handleSubmit}
            onResend={handleResend}
            loading={loading}
          />

          <div className="mt-6 text-center">
            <button
              onClick={() => navigate('/')}
              className="text-sm text-blue-600 hover:text-blue-700 font-semibold transition-colors duration-200"
            >
              Back to Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OTPVerification;
