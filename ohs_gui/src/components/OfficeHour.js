import React, { Component } from 'react';
import './OfficeHour.css';
import Slot from "./Slot"

class OfficeHour extends Component {
  constructor(props) {
    super(props);

    // TODO
    var bookedSlots = new Array(this.props.slotNum);
    for (var i = 0; i < bookedSlots.length; ++i) { bookedSlots[i] = false; }

    this.state = { 
      slotNum : this.props.slotNum,
      bookedSlots: bookedSlots
     }

     this.toggleBooking = this.toggleBooking.bind(this);
  }

  toggleBooking(idx) {
    var lst = this.state.bookedSlots.slice(0);
    lst[idx] = !lst[idx];
    this.setState({bookedSlots: lst});
  }


  render() {
    const slots = this.state.bookedSlots.map((d, i) => 
      <Slot key={i} id={i} toggleBooking={this.toggleBooking} booked={this.state.bookedSlots[i]}>{d} </Slot>);
    
      console.log(this.state.bookedSlots);

    return (
      <div className="office-hour">
        <div className="container">
            {slots}
        </div>
      </div>
    );
  }
}

export default OfficeHour;
