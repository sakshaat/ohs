import ApolloClient from "apollo-boost";

const client = new ApolloClient({
    uri: `${process.env.REACT_APP_INSTRUCTOR_SERVICE_URL || 'http://localhost:8000'}/graphql`
});

export {client};