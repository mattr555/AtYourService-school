jQuery ->
	$('.btn-div').on('click', '.approve-button.btn-danger', ->
		button = $(this)
		user_id = $('#userid').text()
		event_id = button.data 'event-id'
		type = button.data 'type'
		response = $.ajax(
			'/ajax/main/toggle_event_approval.json'
			data:
				'user_id': user_id
				'event_id': event_id
				'type': type
			success: (data) ->
				button.removeClass('btn-danger').addClass('btn-success').html('Approve')
				button.parents('tr').removeClass().addClass('danger')
				button.parents('tr').children('.status-field').html(data.data.status)
			error: ->
				console.log type
				console.log user_id
				console.log event_id
			timeout: 3000
			type: "POST"
			)
		undefined)

	$('.btn-div').on('click', '.approve-button.btn-success', ->
		button = $(this)
		user_id = $('#userid').text()
		event_id = button.data 'event-id'
		type = button.data 'type'
		response = $.ajax(
			'/ajax/main/toggle_event_approval.json'
			data:
				'user_id': user_id
				'event_id': event_id
				'type': type
			success: (data) ->
				button.removeClass('btn-success').addClass('btn-danger').html('Disapprove')
				button.parents('tr').removeClass()
				button.parents('tr').children('.status-field').html(data.data.status)
			timeout: 3000
			type: "POST"
			)
		undefined)

	undefined