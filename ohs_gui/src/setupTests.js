import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import queryMock from './components/utils/queryMock';
import { PROF_BASE_URL } from './components/utils/constants';

configure({ adapter: new Adapter() });

// making prop errors test errors
const originalConsoleError = console.error;

console.error = message => {
  if (/(Failed prop type)/.test(message)) {
    throw new Error(message);
  }

  originalConsoleError(message);
};

/**
 * Initialize our queryMock and pass in the URL you use to make requests to your GraphQL API. */

queryMock.setup(`${PROF_BASE_URL}/graphql`);

/**
 * Jest has no fetch implementation by default. We make sure fetch exists in our tests by using node-fetch here. */

global.fetch = require('node-fetch');
