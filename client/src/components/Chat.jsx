import React from 'react';
import {BaseComponent} from '../BaseComponent';
import moment from 'moment';

export default class Chat extends BaseComponent {
	componentDidMount() {
		// scroll down
		::this.scrollDown();
		this.lastMessage = null;
	}

	componentWillReceiveProps(props) {
		if (!props.messages) return;

		const lastMessage = props.messages[props.messages.length - 1];
		if (lastMessage && this.lastMessage && lastMessage.id !== this.lastMessage.id) {
			::this.scrollDown();
		}

		this.lastMessage = lastMessage;
	}

	scrollDown() {
		const {container} = this.refs;

		let {clientHeight, scrollHeight, scrollTop} = container;

		const THRESHOLD = 10;
		if (scrollTop >= scrollHeight - clientHeight - THRESHOLD) {
			setTimeout(() => {
				container.scrollTop = container.scrollHeight;
			}, 50);
		}
	}

	render() {
		const {messages} = this.props;

		let lastDate = null;

		const content = messages.map(m => {
			let date = moment.utc(m.date).format('D MMM - hh:mm');

			if (date == lastDate) {
				lastDate = date;
				date = '';
			} else {
				lastDate = date;
			}

			return <div className="message" key={m.id}>
				<span className="date">{date}</span>
				<div className="text">{m.text}</div>
			</div>;
		});

		return <div className="chat" ref="container">
			{content}
		</div>;
	}
}
