import React from 'react';
import classnames from 'classnames';

export default class HoverButton extends React.Component {
	render() {
		const {color, icon, children} = this.props;

		const className = classnames('hover-button', color);

		return <div className={className}>
			{children}
			<div className="overlay">
				<button>{icon}</button>
			</div>
		</div>;
	}
}
