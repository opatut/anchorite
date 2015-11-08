import React from 'react';
import classnames from 'classnames';
import {BaseComponent} from '../BaseComponent';

export default class Sprite extends BaseComponent {
	static propTypes = {
		sprite: React.PropTypes.string.isRequired,
		width: React.PropTypes.number.isRequired,
		height: React.PropTypes.number.isRequired,
		frames: React.PropTypes.arrayOf(React.PropTypes.number),
		count: React.PropTypes.number,
		framerate: React.PropTypes.number,

		className: React.PropTypes.string,
	};

	static defaultProps = {
		framerate: 4,
	};

	constructor(...args) {
		super(...args);

		this._interval = null;
		this._accumulator = Math.random();

		this.state = {
			...this.state,
			frame: Math.floor(Math.random() * 100000),
		};
	}

	componentDidMount() {
		this._interval = setInterval(::this.tick, 10);
	}

	componentWillUnmount() {
		if (this._interval) {
			clearInterval(this._interval);
		}
	}

	tick() {
		this._accumulator += 0.01 * this.props.framerate;

		while (this._accumulator > 1) {
			this.setState({
				frame: this.state.frame + 1
			});
			this._accumulator -= 1;
		}

	}

	render() {
		const {width, height, sprite, frames, className, displayUnit, displayWidth: _1, displayHeight: _2, ...props} = this.props;
		let {displayWidth, displayHeight} = this.props;

		if (!this.props.count && !frames) {
			console.warn('Need either count for frames[] for <Sprite/>.');
			return <script />;
		}
		const count = this.props.count || frames.length;

		const {frame} = this.state;
		const currentFrame = frames ? frames[frame % frames.length] : (frame % frames.length);

		const ratio = width/height;

		if (displayWidth) {
			displayHeight = `${displayWidth / ratio}${displayUnit}`;
			displayWidth = `${displayWidth}${displayUnit}`;
		} else if (displayHeight) {
			displayWidth = `${displayHeight * ratio}${displayUnit}`;
			displayHeight = `${displayHeight}${displayUnit}`;
		}

		const style = {
			backgroundPosition: `-${currentFrame*100}% 0px`,
			backgroundSize: `${count * 100}% 100%`,
			backgroundImage: `url(${sprite})`,
			width: displayWidth || width,
			height: displayHeight || height,
		};

		const spacerStyle = {
			paddingBottom: `${height/width*100}%`,
			width: '100%',
		};

		return <div className={classnames('sprite', className)} style={style} {...props}><div style={spacerStyle} /></div>;
	}
}
