import React from 'react';
import classnames from 'classnames';
import {BaseComponent} from '../BaseComponent';
import clock from '../clock';

@clock.listen
export default class ProgressIcon extends BaseComponent {
	render() {
		const {children, start, end, duration, progress, round, tick} = this.props;

		let alpha;

		if (progress !== undefined) {
			alpha = progress;
		} else if (start !== undefined && end !== undefined) {
			alpha = (tick - start) / (end - start);
		} else if (start !== undefined && duration !== undefined) {
			alpha = (tick - start) / duration;
		} else if (end !== undefined && duration !== undefined) {
			let elapsed = tick - (end - duration);
			alpha = elapsed / duration;
		} else {
			console.warn(`ProgressIcon needs more data to function.`);
		}

		alpha = Math.min(1, Math.max(0, alpha));

		alpha = 1 - alpha;

		const className = classnames('progress-icon', {round});

		const y = Math.sin(- alpha*Math.PI*2 - Math.PI/2)*100 + 100;
		const x = Math.cos(- alpha*Math.PI*2 - Math.PI/2)*100 + 100;
		const large = alpha > 0.5;

		const svg = alpha >= 1
			? `<circle cx="100" cy="100" r="100" />`
			: `<path d="M100,100 L100,0 A100,100 0 ${large?1:0},0 ${x},${y} z" />`;

		return <div className={className}>
			{children}
			<div className="overlay">
				<svg viewBox="0 0 200 200" width="100%" height="100%" dangerouslySetInnerHTML={{ __html: svg }} />
			</div>
		</div>;
	}
}
