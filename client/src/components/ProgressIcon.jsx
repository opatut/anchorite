import React from 'react';
import classnames from 'classnames';

export default class ProgressIcon extends React.Component {
	static contextTypes = {
		tick: React.PropTypes.number.isRequired,
	}

	render() {
		const {children, start, end, duration, progress} = this.props;

		let alpha;

		const {tick} = this.context;

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

		const className = classnames('progress-icon');

		const y = Math.sin(alpha*Math.PI*2 - Math.PI/2)*200 + 100;
		const x = Math.cos(alpha*Math.PI*2 - Math.PI/2)*200 + 100;
		const large = alpha > 0.5;

		const svg = `<path d="M100,100 L100,-100 A200,200 0 ${large?1:0},1 ${x},${y} z" />`;

		return <div className={className}>
			{children}
			<div className="overlay">
				<svg viewBox="0 0 200 200" width="100%" height="100%" dangerouslySetInnerHTML={{ __html: svg }} />
			</div>
		</div>;
	}
}
