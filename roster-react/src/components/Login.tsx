import React, { useState } from 'react';
import styled from 'styled-components';

const LoginContainer = styled.div`
  text-align: center;
  margin: auto;
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const Title = styled.h1`
  font-size: 24px;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const Button = styled.button`
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const LoginButtons = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
`;

const ForgotPasswordLink = styled.a`
  text-decoration: none;
  color: #007bff;
  cursor: pointer;
`;


function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // for a real system, send one request and pass the route attributes as variables to the function

  const handleLogin = () => {

    // @ts-ignore
    let csrf = document.getElementsByName("csrf-token")[0].content;

    fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": csrf,
      },
      body: JSON.stringify({ email, password }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Login failed');
      })
      .then((data) => {
        console.log('Login success:', data);
      })
      .catch((error) => {
        console.error('Login error:', error);
      });
  };

  const handleGoogleLogin = () => {

    // @ts-ignore
    let csrf = document.getElementsByName("csrf-token")[0].content;

    fetch('/google/', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
        },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Google login failed');
      })
      .then((data) => {
        // Handle the response as needed
      })
      .catch((error) => {
        console.error('Google login error:', error);
      });
  };

  const handleFacebookLogin = () => {
    // @ts-ignore
    let csrf = document.getElementsByName("csrf-token")[0].content;
  
    // Make a POST request to the Facebook login proxy route
    fetch('/facebook/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": csrf,
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Facebook login failed');
      })
      .then((data) => {
        if (data.redirect_url) {
          // Redirect the user to the Facebook login page
          window.location.href = data.redirect_url;
        } else {
          console.error('Facebook login failed');
        }
      })
      .catch((error) => {
        console.error('Facebook login error:', error);
      });
  };
  
  

  const handleForgotPassword = () => {
    // @ts-ignore
    let csrf = document.getElementsByName("csrf-token")[0].content;

    fetch('/api/reset_password', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify({ email: email })
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Forgot password failed');
      })
      .then((data) => {
        // Handle the response as needed
      })
      .catch((error) => {
        console.error('Forgot password error:', error);
      });
  };

   return (
    <LoginContainer>
      <Title>Login</Title>
      <Input
        type="text"
        placeholder="Email"
        value={email}
        onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setEmail(e.target.value)}
      />
      <Input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setPassword(e.target.value)}
      />
      <Button onClick={handleLogin}>Login</Button>

      <LoginButtons>
        <Button onClick={handleGoogleLogin}>Sign in with Google</Button>
        <Button onClick={handleFacebookLogin}>Sign in with Facebook</Button>
      </LoginButtons>

      <ForgotPasswordLink onClick={handleForgotPassword}>Forgot Password?</ForgotPasswordLink>
    </LoginContainer>
  );

}

export default Login;
