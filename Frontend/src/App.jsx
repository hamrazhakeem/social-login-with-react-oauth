// App.js
import './App.css';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import GoogleButton from 'react-google-button';

function App() {
  // Define the success handler for Google Login
  const handleSuccess = async (codeResponse) => {
    try {
      console.log('Google OAuth Response:', codeResponse);
      const response = await axios.post('http://127.0.0.1:8001/accounts/google-login/', { "code": codeResponse.code });
      console.log('Server Response:', response.data);
    } catch (error) {
      console.error('Error during Google login:', error);
    }
  };

  // Initialize Google Login hook with useGoogleLogin
  const handleGoogleLogin = useGoogleLogin({
    onSuccess: handleSuccess,
    flow: 'auth-code',
  });

  return (
    <div>
      <GoogleButton
        onClick={handleGoogleLogin} // Trigger login when GoogleButton is clicked
        type="dark" // Styling type for the Google button
      />
    </div>
  );
}

export default App;
