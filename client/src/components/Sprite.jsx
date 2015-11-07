import React from 'react';

export default class Sprite extends React.Component {
	static propTypes = {
		framerate: React.PropTypes.number,
		frames: React.PropTypes.arrayOf(React.PropTypes.string).isRequired,
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
		const {frames} = this.props;
		const currentFrame = this.state.frame % frames.length;

		return <div>
			{frames.map((frame, i) => {
				return <img key={i} src={frame} style={{ display: i == currentFrame ? null : 'none' }} />;
			})}
		</div>
	}
}
