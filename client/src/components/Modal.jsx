import React from 'react';
import classnames from 'classnames';
import {BaseComponent} from '../BaseComponent';

export default class Modal extends BaseComponent {
	render() {
		const {children, open, className, onToggle} = this.props;

		return <div className={classnames('modal', {open}, className)}>
			<div className="background" onClick={() => onToggle()}></div>
			<div className="content">
				{children}
			</div>
		</div>;
	}
}
