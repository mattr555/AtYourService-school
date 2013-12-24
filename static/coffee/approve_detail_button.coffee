jQuery ->
	change_hours = (data) ->
		$('#user-status').text(data.data.status)
		old_text = $('#hours').text()
		$('#hours').text(data.data.hours.toString() + old_text.slice(-4))

	$('.button-div').on('click', '.approve-button.btn-danger', (e) ->
		e.stopPropagation()
		button = $(this)
		event_id = button.data 'event-id'
		type = button.data 'type'
		response = $.ajax(
			'/ajax/main/toggle_event_approval.json'
			data:
				'event_id': event_id
				'type': type
			success: (data) ->
				console.log 'disapprove called'
				button.removeClass('btn-danger').addClass('btn-success').html('Approve')
				change_hours(data)
			timeout: 3000
			type: "POST"
			)
		)

	$('.button-div').on('click', '.approve-button.btn-success', (e) ->
		e.stopPropagation()
		button = $(this)
		event_id = button.data 'event-id'
		type = button.data 'type'
		response = $.ajax(
			'/ajax/main/toggle_event_approval.json'
			data:
				'event_id': event_id
				'type': type
			success: (data) ->
				console.log 'approve called'
				button.removeClass('btn-success').addClass('btn-danger').html('Disapprove')
				change_hours(data)
			timeout: 3000
			type: "POST"
			)
		)