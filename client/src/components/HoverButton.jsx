import React from 'react';
import classnames from 'classnames';
import {BaseComponent} from '../BaseComponent';

export default class HoverButton extends BaseComponent {
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
