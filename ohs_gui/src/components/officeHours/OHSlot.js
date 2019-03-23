import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

import React, { Component } from 'react';
import './OHSlot.css';

library.add(faPlus);

class OHSlot extends Component {
  constructor(props) {
    super(props);
    const { booked } = props.booked;
    this.state = {
      booked
    };
  }

  componentWillReceiveProps(nextProps) {
    const { booked } = nextProps;
    this.setState({ booked });
  }

  render() {
    const { booked } = this.state;
    const { id, toggleBooking } = this.props;

    const slotClass = booked ? 'book-button booked' : 'book-button';
    return (
      <div
        className={slotClass}
        onClick={() => toggleBooking(id)}
        role="presentation"
      >
        {booked ? null : (
          <FontAwesomeIcon className="fa-plus slot-info" icon="plus" />
        )}
        {booked ? <h2 className="slot-info">Booked!</h2> : null}
      </div>
    );
  }
}

export default OHSlot;
