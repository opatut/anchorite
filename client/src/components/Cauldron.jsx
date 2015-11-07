import React from 'react';

export default class Cauldron extends React.Component {
	static contextTypes = {
		dispatch: React.PropTypes.func.isRequired,
	}

	render() {
		const {dispatch} = this.context;
		return <div className='cauldron' onClick={() => dispatch({ type: 'collect' })}/>;
	}
}
