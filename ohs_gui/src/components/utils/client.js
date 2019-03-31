import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { setContext } from 'apollo-link-context';
import { InMemoryCache } from 'apollo-cache-inmemory';

const PROF_BASE_URL = `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL ||
  'http://localhost:8000'}`;

const STUDENT_BASE_URL = `${process.env.REACT_APP_STUDENT_SERVICE_URL ||
  'http://localhost:8001'}`;

const getProfClient = () => {
  const httpLink = createHttpLink({
    uri: `${PROF_BASE_URL}/graphql`
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

export { client, PROF_BASE_URL, STUDENT_BASE_URL, getProfClient };
