import Event from './Event';

function Events(data) {
    data = data.data;

    return (
        <>
            <h1>Events</h1>
            <ul>
                {data.map((event) => (
                    <li key={event.id}>
                        <Event event={event} />
                    </li>
                ))}
            </ul>
        </>
    );
}

export default Events;