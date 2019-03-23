import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { setContext } from 'apollo-link-context';
import { InMemoryCache } from 'apollo-cache-inmemory';

const BASE_URL = `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL ||
  'http://localhost:8000'}`;

const getClient = () => {
  const httpLink = createHttpLink({
    uri: `${BASE_URL}/graphql`
  });

  const authLink = setContext((_, { headers }) => {
    // get the authentication token from local storage if it exists
    const token = window.sessionStorage.getItem('token');
    // return the headers to the context so httpLink can read them
    return {
      headers: {
        ...headers,
        Authorization: token ? `Bearer ${token}` : ''
      }
    };
  });

  const client = new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache()
  });

  return client;
};

const client = null;

export { client, BASE_URL, getClient };
