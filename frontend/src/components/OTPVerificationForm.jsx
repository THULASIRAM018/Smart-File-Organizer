import { useState, useEffect } from 'react';
import { Shield, RefreshCw } from 'lucide-react';

const OTPVerificationForm = ({ email, onSubmit, onResend, loading }) => {
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [timer, setTimer] = useState(60);
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    let interval;
    if (timer > 0 && !canResend) {
      interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setCanResend(true);
    }
    return () => clearInterval(interval);
  }, [timer, canResend]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!otp) {
      setError('OTP is required');
      return;
    }

    if (otp.length !== 6) {
      setError('OTP must be 6 digits');
      return;
    }

    if (!/^\d+$/.test(otp)) {
      setError('OTP must contain only numbers');
      return;
    }

    onSubmit(otp);
  };

  const handleResend = () => {
    setTimer(60);
    setCanResend(false);
    setOtp('');
    onResend();
  };

  const handleOtpChange = (e) => {
    const value = e.target.value.replace(/\D/g, '');
    if (value.length <= 6) {
      setOtp(value);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="text-center mb-6">
        <p className="text-gray-600">
          Enter the 6-digit OTP sent to{' '}
          <span className="font-semibold text-blue-600">{email}</span>
        </p>
      </div>

      <div>
        <label htmlFor="otp" className="block text-sm font-semibold text-gray-700 mb-2">
          One-Time Password
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Shield className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            id="otp"
            value={otp}
            onChange={handleOtpChange}
            maxLength={6}
            className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-4 focus:ring-blue-300 focus:border-blue-500 transition-all duration-200 outline-none text-center text-2xl font-bold tracking-widest"
            placeholder="000000"
            disabled={loading}
          />
        </div>
        {error && <p className="mt-2 text-sm text-red-500 font-medium">{error}</p>}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-500 to-green-500 text-white py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-green-600 transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
      >
        {loading ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            <span>Verifying...</span>
          </>
        ) : (
          <span>Verify OTP</span>
        )}
      </button>

      <div className="text-center">
        {canResend ? (
          <button
            type="button"
            onClick={handleResend}
            className="inline-flex items-center space-x-2 text-orange-600 hover:text-orange-700 font-semibold transition-colors duration-200"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Resend OTP</span>
          </button>
        ) : (
          <p className="text-gray-500">
            Resend OTP in <span className="font-semibold text-yellow-600">{timer}s</span>
          </p>
        )}
      </div>
    </form>
  );
};

export default OTPVerificationForm;
