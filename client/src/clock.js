import React from 'react';
import {BaseComponent} from './BaseComponent';

let listeners = [];

export function listen(Component) {
	class TickedComponent extends BaseComponent {
		constructor() {
			super(...arguments);
			this.state = {
				...this.state,
				tick: 0,
			}
		}

		render() {
			return <Component {...this.props} tick={this.state.tick} />;
		}

		componentDidMount() {
			listeners.push(this);
		}

		componentWillUnmount() {
			listeners = listeners.filter(l => l != this);
		}

		setTick(tick) {
			this.setState({tick});
		}
	}

	return TickedComponent;
}

export function set(tick) {
	listeners.forEach((listener) => {
		listener.setTick(tick);
	});
}

export default {
	listen,
	set
};
