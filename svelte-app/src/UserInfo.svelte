<script>
    import { user } from './store.js';
    let userData;
    const unsubscribe = user.subscribe(value => {
      userData = value;
    });
  </script>
  
  {#if userData}
    <h2>Welcome, {userData.token}!</h2>
    <!-- Display other user information here -->
  {:else}
    {console.log(userData)}
    <p>Please log in to view user information.</p>
  {/if}