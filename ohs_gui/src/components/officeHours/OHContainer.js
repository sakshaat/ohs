import React, { Component } from 'react';
import shortid from 'shortid';

import './OHContainer.css';
import OHSlot from './OHSlot';

class OHContainer extends Component {
  constructor(props) {
    super(props);

    const { slotNum } = this.props;

    // TODO MAY BE AN ISSUE HERE
    const bookedSlots = new Array(slotNum);
    for (let i = 0; i < bookedSlots.length; i += 1) {
      bookedSlots[i] = false;
    }

    this.state = {
      bookedSlots
    };

    this.toggleBooking = this.toggleBooking.bind(this);
  }

  toggleBooking(idx) {
    const { bookedSlots } = this.state;
    const lst = bookedSlots.slice(0);

    // negate that index
    lst[idx] = !lst[idx];
    this.setState({ bookedSlots: lst });
  }

  render() {
    const { bookedSlots } = this.state;
    const slots = bookedSlots.map((d, i) => (
      <OHSlot
        key={shortid.generate()}
        id={i}
        toggleBooking={this.toggleBooking}
        booked={bookedSlots[i]}
      >
        {d}{' '}
      </OHSlot>
    ));

    return (
      <div className="office-hour-cont">
        <div className="container">{slots}</div>
      </div>
    );
  }
}

export default OHContainer;
