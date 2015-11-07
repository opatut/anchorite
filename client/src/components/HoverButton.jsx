import React from 'react';
import classnames from 'classnames';

export default class HoverButton extends React.Component {
	render() {
		const {color, icon, children, onClick, title} = this.props;

		const className = classnames('hover-button', color);

		return <div className={className} title={title}>
			{children}
			<div className="overlay" {...{onClick}}>
				<button>{icon}</button>
			</div>
		</div>;
	}
}
