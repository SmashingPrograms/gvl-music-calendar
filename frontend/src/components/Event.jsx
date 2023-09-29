function Event(event) {
    event = event.event;
    const title = event.title;
    const description = event.description;
    const location = event.location;
    const startTime = event.start;
    const endTime = event.end;
    const attachments = event.attachments;
    

    return (
        <li>
            <h1>{title}</h1>
            <p>{startTime}</p>
            {
                location
                ?
                <p>{location}</p>
                :
                <p>Greenville, SC</p>
            }
            {
                attachments
                &&
                <ul>
                    {attachments.map((attachmentId) => (
                        <li key={attachmentId}>
                            <img src={`https://drive.google.com/file/d/${attachmentId}`} />
                        </li>
                    ))}
                </ul>
            }
            {
                description
                ?
                <p>{description}</p>
                :
                <p>No description provided.</p>
            }
        </li>
    );
}

export default Event;