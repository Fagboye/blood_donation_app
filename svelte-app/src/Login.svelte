<script>
    import { user } from './store.js'
    let username = '';
    let password = '';
  
    const handleLogin = async () => {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });
      const data = await response.json();
      user.set(data); // Store user information in the user store
    };
  </script>
  
  <form on:submit={handleLogin}>
    <input type="text" bind:value={username} placeholder="Username">
    <input type="password" bind:value={password} placeholder="Password">
    <button type="submit">Login</button>
  </form>