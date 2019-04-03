import React, { PureComponent } from 'react';
import shortid from 'shortid';

import './OHContainer.css';
import OHSlot from './OHSlot';

class OHContainer extends PureComponent {
  render() {
    const { bookedSlots, toggleBooking, showBooked } = this.props;
    const slots = bookedSlots.map((d, i) => (
      <OHSlot
        key={shortid.generate()}
        id={i}
        toggleBooking={toggleBooking}
        booked={bookedSlots[i]}
        showBooked={showBooked}
      />
    ));

    return (
      <div className="office-hour-cont">
        <div className="container">{slots}</div>
      </div>
    );
  }
}

export default OHContainer;
